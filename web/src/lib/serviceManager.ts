import ApiClient from "./services/apiClient.ts";
import SessionManager from "./services/sessionManager.ts";

export default class ServiceManager {

    public static createApiClient() {
        const jwt = localStorage.getItem('jwt');
        const baseUrl = `${window.location.protocol}//${window.location.hostname}:5090/api/v1`;
        return new ApiClient(baseUrl, jwt);
    }

    public static createSessionManager() {
        const apiClient = ServiceManager.createApiClient();
        return new SessionManager(apiClient);
    }

}
