import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import App from './App';

// Create a query client for tests
const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

describe('App', () => {
  it('renders TaskFlow app header with data', async () => {
    // Mock successful API call with sample data
    const mockTasks: any[] = [];
    (globalThis as any).fetch = vi.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve(mockTasks),
        ok: true,
      })
    );

    const queryClient = createTestQueryClient();

    render(
      <QueryClientProvider client={queryClient}>
        <App />
      </QueryClientProvider>
    );

    // Wait for loading to finish and check header is rendered
    await waitFor(() => {
      expect(screen.getByText('TaskFlow')).toBeTruthy();
    });

    expect(screen.getByText('Kanban-style task management')).toBeTruthy();
  });

  it('shows connection error when backend is down', async () => {
    const queryClient = createTestQueryClient();

    // Mock fetch to simulate network error
    (globalThis as any).fetch = vi.fn(() =>
      Promise.reject(new Error('Network error'))
    );

    render(
      <QueryClientProvider client={queryClient}>
        <App />
      </QueryClientProvider>
    );

    // Should show connection error message
    expect(await screen.findByText('Connection Error')).toBeTruthy();
  });
});