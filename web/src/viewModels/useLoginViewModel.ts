import { useState } from "react";
import SessionManager from "../lib/services/sessionManager.ts";

const useLoginViewModel = (sessionManager: SessionManager) => {
    const [loginError, setLoginError] = useState<string | null>(null);

    const loginPlayer = (username: string, password: string) => {
        setLoginError(null);

        sessionManager.login(username, password).then((response) => {
            if (response.success) {
                window.location.reload();
            } else {
                setLoginError(response.error);
            }
        });
    }

    return {
        loginError,
        loginPlayer,
    }
}

export default useLoginViewModel;