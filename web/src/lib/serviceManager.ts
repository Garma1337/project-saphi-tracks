import ApiClient from "./services/apiClient.ts";
import SessionManager from "./services/sessionManager.ts";

export default class ServiceManager {

    public static createApiClient() {
        const jwt = localStorage.getItem('jwt');
        return new ApiClient(`http://127.0.0.1:5090/api/v1`, jwt);
    }

    public static createSessionManager() {
        const apiClient = ServiceManager.createApiClient();
        return new SessionManager(apiClient);
    }

}
