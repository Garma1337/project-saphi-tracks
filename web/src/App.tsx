import {Route, Routes} from 'react-router-dom'
import './App.css'
import AppRoutes from './routes'
import Layout from "./views/layout/Layout.tsx";
import IndexView from './views/indexView/IndexView.tsx';
import {useEffect, useState} from "react";
import useStore from './store.ts';
import ApiClient from "./lib/apiClient.ts";
import CustomTrackListView from "./views/customTrackListView/CustomTrackListView.tsx";
import UserListView from "./views/userListView/UserListView.tsx";
import UserPageView from "./views/userPageView/UserPageView.tsx";
import ToolsView from "./views/toolsView/ToolsView.tsx";
import TutorialView from "./views/tutorialView/TutorialView.tsx";
import CustomTrackCreateView from "./views/customTrackCreateView/CustomTrackCreateView.tsx";

function App() {
    const setSettings = useStore(state => state.setSettings);
    const setTags = useStore(state => state.setTags);
    const [apiClient, setApiClient] = useState<ApiClient | null>(null);

    useEffect(() => {
        setApiClient(new ApiClient('http://localhost:5000/api/v1'));
    }, []);

    useEffect(() => {
        if (apiClient) {
            apiClient.findSettings(null, null, null, null, null).then(query => setSettings(query.items));
        }
    }, [apiClient, setSettings]);

    useEffect(() => {
        if (apiClient) {
            apiClient.findTags(null, null, null, null).then(query => setTags(query.items));
        }
    }, [apiClient, setTags]);

    return (
        <Routes>
            <Route path={AppRoutes.IndexPage} element={<Layout/>}>
                <Route index element={<IndexView/>}/>
                <Route path={AppRoutes.CustomTrackCreatePage} element={<CustomTrackCreateView/>}/>
                <Route path={AppRoutes.CustomTrackListPage} element={<CustomTrackListView/>}/>
                <Route path={AppRoutes.ToolsPage} element={<ToolsView/>}/>
                <Route path={AppRoutes.TutorialPage} element={<TutorialView/>}/>
                <Route path={AppRoutes.UserListPage} element={<UserListView/>}/>
                <Route path={AppRoutes.UserDetailPage} element={<UserPageView/>}/>
            </Route>
        </Routes>
    )
}

export default App;