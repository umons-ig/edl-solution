/// <reference types="vitest" />
import { render, screen } from '@testing-library/react'
import App from './App'

describe('App', () => {
  it('renders the main heading', () => {
    render(<App />)

    const heading = screen.getByText('TaskFlow 📋')
    expect(heading).toBeInTheDocument()
  })

  it('renders the subtitle', () => {
    render(<App />)

    const subtitle = screen.getByText('Your Task Management Dashboard')
    expect(subtitle).toBeInTheDocument()
  })

  it('renders the kanban board placeholder', () => {
    render(<App />)

    const placeholder = screen.getByText('Kanban Board Coming Soon')
    expect(placeholder).toBeInTheDocument()
  })
})