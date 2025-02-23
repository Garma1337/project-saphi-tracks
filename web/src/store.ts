import {create, StateCreator} from 'zustand';
import {devtools} from 'zustand/middleware';

export type Store<T extends object> = StateCreator<T, [['zustand/devtools', never]], [], T>;

export type AppState = {
    apiEndpoint: string;
    setApiEndpoint: (apiEndpoint: string) => void;
    jwt: string;
    setJwt: (jwt: string) => void;
    currentUser: any;
    setCurrentUser: (currentUser: any) => void;
    settings: any[];
    setSettings: (settings: any) => void;
    tags: any[];
    setTags: (tags: any) => void;
}

const createStore: Store<AppState> = (set) => ({
    apiEndpoint: 'http://localhost:5000/api',
    setApiEndpoint: (apiEndpoint: string) => set(() => ({ apiEndpoint }), false, 'setApiEndpoint'),
    jwt: '',
    setJwt: (jwt: string) => set(() => ({ jwt }), false, 'setJwt'),
    currentUser: null,
    setCurrentUser: (currentUser: any) => set(() => ({ currentUser }), false, 'setCurrentUser'),
    tags: [],
    setTags: (tags: any) => set(() => ({ tags }), false, 'setTags'),
    settings: [],
    setSettings: (settings: any) => set(() => ({ settings }), false, 'setSettings'),
});

const useStore = create<AppState>()(
  devtools(
    (...storeApi) => ({
      ...createStore(...storeApi),
    }),
    { name: 'sharedStore' },
  ),
);

export default useStore;
