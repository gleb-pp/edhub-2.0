import { zodResolver } from '@hookform/resolvers/zod'
import { LoginData } from '../types/type'
import { LoginSchema } from './LoginSchema'
import { useForm } from 'react-hook-form'

export const useLogin = () => {
  const { register, handleSubmit, reset } = useForm<LoginData>({
    resolver: zodResolver(LoginSchema),
    mode: 'onChange',
  })

  const onSubmit = async (data: LoginData) => {
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
  }
}
