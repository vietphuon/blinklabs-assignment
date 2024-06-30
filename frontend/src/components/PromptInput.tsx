// components/PromptInput.tsx
import { useState } from 'react'
import { Input, Button, VStack } from '@chakra-ui/react'

interface PromptInputProps {
  onSubmit: (prompt: string) => void
  isLoading: boolean
}

export const PromptInput: React.FC<PromptInputProps> = ({ onSubmit, isLoading }) => {
  const [prompt, setPrompt] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(prompt)
  }

  return (
    <form onSubmit={handleSubmit}>
      <VStack spacing={4}>
        <Input
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter your coding question"
          size="lg"
        />
        <Button type="submit" colorScheme="blue" isLoading={isLoading} loadingText="Generating">
          Generate Code
        </Button>
      </VStack>
    </form>
  )
}