import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
    event.locals.authToken = event.cookies.get('auth_token') || null;

    return resolve(event);
}
