import { ChakraProvider } from '@chakra-ui/react'
import type { AppProps } from 'next/app'
import ErrorBoundary from '../components/ErrorBoundary'

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ChakraProvider>
        <ErrorBoundary>
            <Component {...pageProps} />
        </ErrorBoundary>
    </ChakraProvider>
  )
}

export default MyApp