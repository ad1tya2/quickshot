import { writable } from 'svelte/store';

function createLocalStorageStore(key, initialValue) {
    const storedValue = localStorage.getItem(key);
    const initial = storedValue ? JSON.parse(storedValue) : initialValue;

    const { subscribe, set, update } = writable(initial);

    return {
        subscribe,
        set: value => {
            localStorage.setItem(key, JSON.stringify(value));
            set(value);
        },
        update,
    };
}

export default createLocalStorageStore;