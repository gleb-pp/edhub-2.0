import z from 'zod'
import { LoginSchema } from '../models/LoginSchema'

export type LoginData = z.infer<typeof LoginSchema>
