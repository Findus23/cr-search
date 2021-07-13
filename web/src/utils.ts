export const baseURL = (process.env.NODE_ENV === "production") ? "/api/" : "http://127.0.0.1:5000/api/";

const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");

export const reducedMotion = (!mediaQuery || mediaQuery.matches);


const wait = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));
