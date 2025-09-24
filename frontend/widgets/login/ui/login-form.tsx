'use client'
import { Card } from '@/shared/ui/card/card'
import clsx from 'clsx'
import React from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { Input } from '@/shared/ui/input/input'
import { Button } from '@/shared/ui/button/button'
import { useLogin } from '../models/useLogin'

interface Props {
  className?: string
}

export const LoginForm: React.FC<Props> = ({ className }) => {
  const { register, handleSubmit } = useLogin()
  return (
    <Card
      className={clsx(
        'w-[25%] h-fit px-8 py-10 text-dark !rounded-2xl !shadow-md',
        className,
      )}
    >
      <div className="flex flex-col items-center justify-center font-light">
        <Image
          className="size-18"
          src={'/logo.svg'}
          alt={'edhub'}
          width={72}
          height={72}
        />
        <h1 className="text-3xl mb-2 mt-3">
          Welcome to <b>Edhub</b>
        </h1>
        <p className="text-lg">
          Don't have an account?{' '}
          <Link className="hover:underline text-[#43adb4]" href={'#'}>
            Sign up
          </Link>
        </p>
      </div>
      <form onSubmit={handleSubmit} noValidate className="mt-3 text-dark/80">
        <div>
          <label className="text-sm" htmlFor="email">
            Email
          </label>
          <Input
            {...register('email')}
            className="py-3 px-5 mt-1 text-md flex items-center justify-between"
            type="text"
            name="email"
            id="email"
            placeholder="Enter your email..."
          />
        </div>
        <div className="mt-4 mb-7">
          <label
            className="text-sm flex items-center justify-between"
            htmlFor="password"
          >
            Password
            <Button className="hover:underline text-dark/80" variant="clean">
              Forgot your password?
            </Button>
          </label>
          <Input
            {...register('password')}
            className="py-3 px-5 mt-1 text-md"
            type="password"
            name="password"
            id="password"
            placeholder="Enter your password..."
          />
        </div>
        <div>
          <Button className="w-full py-3 rounded-md font-light text-lg mb-5">
            Login
          </Button>
          <p className="text-center w-[65%] mx-auto text-sm font-light">
            By clicking Login, you agree to our{' '}
            <Button
              className="inline hover:underline text-dark/50"
              variant="clean"
            >
              Terms of Service
            </Button>{' '}
            and{' '}
            <Button
              className="inline hover:underline text-dark/50"
              variant="clean"
            >
              Privacy Policy
            </Button>
            .
          </p>
        </div>
      </form>
    </Card>
  )
}
