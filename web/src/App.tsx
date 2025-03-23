import {Route, Routes} from 'react-router-dom'
import './App.css'
import AppRoutes from './routes'
import Layout from "./views/layout/Layout.tsx";
import IndexView from './views/indexView/IndexView.tsx';
import {useEffect} from "react";
import useStore from './store.ts';
import ApiClient from "./lib/apiClient.ts";
import CustomTrackListView from "./views/customTrackListView/CustomTrackListView.tsx";
import UserListView from "./views/userListView/UserListView.tsx";
import UserPageView from "./views/userPageView/UserPageView.tsx";
import ToolsView from "./views/toolsView/ToolsView.tsx";
import TutorialView from "./views/tutorialView/TutorialView.tsx";
import CustomTrackCreateView from "./views/customTrackCreateView/CustomTrackCreateView.tsx";
import LoginView from "./views/loginView/LoginView.tsx";
import ServiceManager from "./lib/serviceManager.ts";
import CustomTrackPageView from "./views/customTrackPageView/CustomTrackPageView.tsx";

function App() {
    const apiClient: ApiClient = ServiceManager.createApiClient();

    const setCurrentUser = useStore(state => state.setCurrentUser);
    const setSettings = useStore(state => state.setSettings);
    const setTags = useStore(state => state.setTags);

    useEffect(() => {
        apiClient.getSession().then(response => setCurrentUser(response.current_user));
    }, [setCurrentUser]);

    useEffect(() => {
        apiClient.findSettings(null, null, null, null, null).then(query => setSettings(query.items));
    }, [setSettings]);

    useEffect(() => {
        apiClient.findTags(null, null, null, null).then(query => setTags(query.items));
    }, [setTags]);

    return (
        <Routes>
            <Route path={AppRoutes.IndexPage} element={<Layout/>}>
                <Route index element={<IndexView/>}/>
                <Route path={AppRoutes.CustomTrackCreatePage} element={<CustomTrackCreateView/>}/>
                <Route path={AppRoutes.CustomTrackListPage} element={<CustomTrackListView/>}/>
                <Route path={AppRoutes.CustomTrackDetailPage} element={<CustomTrackPageView/>}/>
                <Route path={AppRoutes.LoginPage} element={<LoginView/>}/>
                <Route path={AppRoutes.ToolsPage} element={<ToolsView/>}/>
                <Route path={AppRoutes.TutorialPage} element={<TutorialView/>}/>
                <Route path={AppRoutes.UserListPage} element={<UserListView/>}/>
                <Route path={AppRoutes.UserDetailPage} element={<UserPageView/>}/>
            </Route>
        </Routes>
    )
}

export default App;