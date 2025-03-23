import ApiClient from "./apiClient.ts";

export default class ServiceManager {

    public static createApiClient() {
        const jwt = localStorage.getItem('jwt');
        return new ApiClient(`http://127.0.0.1:5000/api/v1`, jwt);
    }

}
