'use client'
import { Card } from '@/shared/ui/card/card'
import clsx from 'clsx'
import React from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { Input } from '@/shared/ui/input/input'
import { Button } from '@/shared/ui/button/button'
import { useSignup } from '../models/useSignup'

interface Props {
  className?: string
}

export const SignupForm: React.FC<Props> = ({ className }) => {
  const { register, handleSubmit, errors, isSubmitting, isValid } = useSignup()
  return (
    <Card
      className={clsx(
        'min-w-[25%] w-[25%] h-fit px-8 py-10 text-dark !rounded-2xl !shadow-md',
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
          Already have an account?{' '}
          <Link className="hover:underline text-[#43adb4]" href={'#'}>
            Log in
          </Link>
        </p>
      </div>
      <form onSubmit={handleSubmit} noValidate className="mt-3 text-dark/80">
        <div>
          <label className="text-sm" htmlFor="name">
            Your name
          </label>
          <Input
            {...register('name')}
            className="py-3 px-5 mt-1 text-md flex items-center justify-between"
            type="text"
            name="name"
            id="name"
            placeholder="Enter your name..."
            aria-invalid={errors.name ? 'true' : 'false'}
          />
        </div>
        <div className="mt-4">
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
            aria-invalid={errors.email ? 'true' : 'false'}
          />
        </div>
        <div className="mt-4">
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
            aria-invalid={errors.password ? 'true' : 'false'}
          />
        </div>
        <p className="mt-4 text-center text-ui-red text-xs">
          {errors.name?.message ??
            errors.email?.message ??
            errors.password?.message}
        </p>
        <div className="mt-6">
          <Button
            type="submit"
            disabled={isSubmitting}
            className="w-full py-3 rounded-md font-light text-lg mb-5"
          >
            {isSubmitting ? 'Creating account...' : 'Signup'}
          </Button>
          <p className="text-center w-[65%] mx-auto text-sm font-light">
            By clicking continue, you agree to our{' '}
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
