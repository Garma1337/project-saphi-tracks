import {create, StateCreator} from 'zustand';
import {devtools} from 'zustand/middleware';

export type Store<T extends object> = StateCreator<T, [['zustand/devtools', never]], [], T>;

export type AppState = {
    currentUser: any;
    setCurrentUser: (currentUser: any) => void;
    settings: any[];
    setSettings: (settings: any) => void;
    tags: any[];
    setTags: (tags: any) => void;
}

const createStore: Store<AppState> = (set) => ({
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
