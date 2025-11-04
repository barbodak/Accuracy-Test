export function getCookies(name: string): string | null {
    if (typeof document === 'undefined')
        return null;
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        let res = parts.pop()?.split(';').shift() || null;
        return res;
    }
    return null;
}

export function setCookies(name: string, value: string, age: number): void {
    if (typeof document === 'undefined')
        return;
    const isSecure = window.location.protocol === 'https:';
    const secureFlag = isSecure ? '; Secure' : '';
    const maxAgeFlag = age ? `; max-age=${age}` : '';

    document.cookie = `${name}=${value}; path=/; ${maxAgeFlag}; SameSite=Lax; ${secureFlag}`;
}

export function deleteCookies(name: string): void {
    if (typeof document === 'undefined')
        return;
    document.cookie = `${name}=; path=/; max-age=0`;
}
