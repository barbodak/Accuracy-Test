// src/lib/utils/timer.ts
import { tweened } from "svelte/motion";
import { writable } from "svelte/store";

export function createQuizTimer(startTime: string | Date, durationInSeconds: number) {
    const qdate = new Date(startTime).valueOf();
    const now = new Date().valueOf();
    const timeElapsed = Math.floor((now - qdate) / 1000);
    const remainingTime = Math.max(durationInSeconds - timeElapsed, 0);

    const timer = tweened(remainingTime, { duration: 1000 });
    const isTimeUp = writable(false);

    let interval: ReturnType<typeof setInterval>;

    // We create a start function to be called inside onMount
    const start = () => {
        interval = setInterval(() => {
            timer.update((t) => {
                if (t <= 0) {
                    clearInterval(interval);
                    isTimeUp.set(true);
                    return 0;
                }
                return t - 1;
            });
        }, 1000);
    };

    return {
        timer,
        isTimeUp,
        start, // Expose start function
        destroy: () => clearInterval(interval)
    };
}

