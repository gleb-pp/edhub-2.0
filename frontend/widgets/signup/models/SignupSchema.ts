import { z } from 'zod'

export const SignupSchema = z.object({
  name: z
    .string()
    .min(1, 'Name must be at least 2 characters')
    .max(80, 'Name must be a maximum of 80 characters.')
    .regex(
      /^[A-Za-z0-9_ ]+$/,
      'Only letters, numbers, underscores and spaces allowed',
    ),
  email: z.email('Invalid email address'),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters long')
    .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
    .regex(/[0-9]/, 'Password must contain at least one digit')
    .regex(
      /[^A-Za-z0-9]/,
      'Password must contain at least one special character',
    ),
})
