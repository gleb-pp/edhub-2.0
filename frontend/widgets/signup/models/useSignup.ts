import { useForm } from 'react-hook-form'
import { SignupData } from '../types/type'
import { zodResolver } from '@hookform/resolvers/zod'
import { SignupSchema } from './SignupSchema'

export const useSignup = () => {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting, isValid },
    reset,
  } = useForm<SignupData>({
    resolver: zodResolver(SignupSchema),
    mode: 'onChange',
  })

  const onSubmit = async (data: SignupData) => {
    try {
      console.log(data)

      reset()
    } catch (e) {
      console.log(e)
    }
  }

  return {
    register,
    handleSubmit: handleSubmit(onSubmit),
    errors,
    isSubmitting,
    isValid,
  }
}
