import { useState } from 'react'
import { generateCode, CodeResponse } from '../services/api'

export const useCodeGeneration = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<CodeResponse | null>(null)

  const generate = async (prompt: string) => {
    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await generateCode(prompt)
      setResult(response)
    } catch (err) {
      setError('An error occurred while generating the code')
    } finally {
      setIsLoading(false)
    }
  }

  return { isLoading, error, result, generate }
}