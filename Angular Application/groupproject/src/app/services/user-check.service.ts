import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environment} from "../../environments/environment.development";
import {lastValueFrom} from "rxjs";


@Injectable({
  providedIn: 'root'
})
export class UserCheckService {
  uri = environment.API_BASE_URL
  constructor(
    private http: HttpClient
  ) { }

  /**
   * Gets the funds of the user
   * @param uid
   */
  async getUserFunds(uid: string): Promise<any> {
    const fundsURI = this.uri + "/userfunds";
    try {
      const response = await lastValueFrom(this.http.post<any>(fundsURI, {uid}));
      console.log('Funds check response:', response);
      return response;
    } catch (error) {
      console.error('Error fetching user funds:', error);
      throw error;
    }
  }

  /**
   * Checks if the user is an admin, returns boolean
   * @param uid
   */
  async isUserAnAdmin(uid: string): Promise<boolean> {
    const isAdminURI = this.uri + "/useradmin";
    try {
      const response = await lastValueFrom(this.http.post<any>(isAdminURI, {uid}));
      return response.response === "yes";
    } catch (error) {
      console.error("Error checking admin status:", error);
    }
    return false;
  }


  /**
   * Checks if the user is a manager, returns boolean
   * @param uid
   */
  async isUserAnManager(uid: string): Promise<boolean> {
    const isManagerURI = this.uri + "/usermanager";
    try {
      const response = await lastValueFrom(this.http.post<any>(isManagerURI, { uid }));
      return response.response === "yes";
    } catch (error) {
      console.error("Error checking manager status:", error);
    }
    return false;
  }

}
