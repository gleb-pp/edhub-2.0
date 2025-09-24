import z from 'zod'
import { SignupSchema } from '../models/SignupSchema'

export type SignupData = z.infer<typeof SignupSchema>
