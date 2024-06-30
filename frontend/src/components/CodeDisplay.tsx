import { Box, Text, Code } from '@chakra-ui/react'

interface CodeDisplayProps {
  code: string
  explanation: string
}

export const CodeDisplay: React.FC<CodeDisplayProps> = ({ code, explanation }) => {
  return (
    <Box mt={4}>
      <Text fontWeight="bold" mb={2}>Generated Code:</Text>
      <Code p={3} borderRadius="md" bg="gray.100" display="block" whiteSpace="pre-wrap">
        {code}
      </Code>
      <Text fontWeight="bold" mt={4} mb={2}>Explanation:</Text>
      <Text>{explanation}</Text>
    </Box>
  )
}