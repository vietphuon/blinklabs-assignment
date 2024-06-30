// components/ErrorBoundary.tsx
import React, { ErrorInfo, ReactNode } from 'react'
import { Box, Heading, Text } from '@chakra-ui/react'

interface ErrorBoundaryProps {
  children: ReactNode
}

interface ErrorBoundaryState {
  hasError: boolean
}

class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(_: Error): ErrorBoundaryState {
    return { hasError: true }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <Box textAlign="center" py={10} px={6}>
          <Heading as="h2" size="xl" mt={6} mb={2}>
            Oops! Something went wrong.
          </Heading>
          <Text color={'gray.500'}>
            We&apos;re sorry for the inconvenience. Please try refreshing the page.
          </Text>
        </Box>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary