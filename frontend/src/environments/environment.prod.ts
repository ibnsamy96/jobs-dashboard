import { $env } from 'src/typing.d';

export const environment = {
  production: true,
  X_API_KEY: $env.API_KEY,
};
