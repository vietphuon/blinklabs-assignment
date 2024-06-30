// pages/index.tsx
import Head from 'next/head'
import { Container, VStack, Heading, Text, Alert, AlertIcon } from '@chakra-ui/react'
import { PromptInput } from '../components/PromptInput'
import { CodeDisplay } from '../components/CodeDisplay'
import { useCodeGeneration } from '../hooks/useCodeGeneration'
import { Layout } from '../components/Layout'

export default function Home() {
  const { isLoading, error, result, generate } = useCodeGeneration()

  return (
    <Layout>
      <Container maxW="container.md" py={8}>
        <Head>
          <title>AI Coding Tutor</title>
          <meta name="description" content="AI-powered coding tutor" />
          <link rel="icon" href="/favicon.ico" />
        </Head>

        <VStack spacing={8} align="stretch">
          <Heading as="h1" size="2xl" textAlign="center">
            AI Coding Tutor
          </Heading>
          <Text textAlign="center">
            Ask a coding question, and our AI will generate a JavaScript function for you!
          </Text>

          <PromptInput onSubmit={generate} isLoading={isLoading} />

          {error && (
            <Alert status="error">
              <AlertIcon />
              {error}
            </Alert>
          )}

          {result && <CodeDisplay code={result.code} explanation={result.explanation} />}
        </VStack>
      </Container>
    </Layout>
  )
}