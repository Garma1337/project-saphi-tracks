import AppRoutes from "../routes.tsx";
import SessionManager from "../lib/services/sessionManager.ts";
import {useNavigate} from "react-router-dom";

const useLayoutViewModel = (sessionManager: SessionManager) => {
    const navigate = useNavigate();

    const logoutPlayer = () => {
        sessionManager.logout().then(() => {
            window.location.reload();
            navigate(AppRoutes.IndexPage);
        });
    }

    return { logoutPlayer }
}

export default useLayoutViewModel;