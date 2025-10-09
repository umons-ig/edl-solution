// Test setup file
import { vi } from 'vitest'
import '@testing-library/jest-dom'

// Mock fetch for testing
;(globalThis as any).fetch = vi.fn()

// Mock matchMedia which is not implemented in jsdom
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(), // deprecated
    removeListener: vi.fn(), // deprecated
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
})

// Add any other global test setup here