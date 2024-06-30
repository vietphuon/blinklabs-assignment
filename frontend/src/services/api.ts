import axios from 'axios'

const API_URL = 'http://localhost:8080'

export interface CodeResponse {
  code: string
  explanation: string
}

export const generateCode = async (prompt: string): Promise<CodeResponse> => {
  const response = await axios.post<CodeResponse>(`${API_URL}/generate_code`, { prompt })
  return response.data
}