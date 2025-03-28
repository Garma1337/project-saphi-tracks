import ApiClient from "./apiClient.ts";
import {LoginResponse, SessionResponse} from "./../api/response.ts";

export default class SessionManager {
    protected apiClient: ApiClient;

    constructor(apiClient: ApiClient) {
        this.apiClient = apiClient;
    }

    public async getSession(): Promise<SessionResponse> {
        return await this.apiClient.getSession();
    }

    public async login(username: string, password: string): Promise<LoginResponse> {
        const response = await this.apiClient.login(username, password);

        if (response.success) {
            localStorage.setItem('jwt', String(response.access_token));
        }

        return response;
    }

    public async logout(): Promise<SessionResponse> {
        localStorage.removeItem('jwt');
        return await this.apiClient.getSession();
    }

}
