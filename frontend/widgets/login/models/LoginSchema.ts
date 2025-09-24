import { z } from 'zod'

export const LoginSchema = z.object({
  email: z.email('Invalid email address'),
  password: z.string(),
})
