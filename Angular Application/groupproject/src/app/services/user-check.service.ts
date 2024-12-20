import { Injectable } from '@angular/core';
import { Firestore, doc, getDoc } from '@angular/fire/firestore';

@Injectable({
  providedIn: 'root'
})
export class UserCheckService {

  constructor(private firestore: Firestore) { }

  /**
   * Checks if the user is an admin, returns boolean
   * @param uid
   */
  async isUserAnAdmin(uid: string): Promise<boolean> {
    const adminDocument = doc(this.firestore, 'admins', uid);
    const adminDocumentResult = await getDoc(adminDocument);
    return adminDocumentResult.exists();
  }

  /**
   * Checks if the user is a manager, returns boolean
   * @param uid
   */
  async isUserAnManager(uid: string): Promise<boolean> {
    const managerDocument = doc(this.firestore, 'managers', uid);
    const managerDocumentResult = await getDoc(managerDocument);
    return managerDocumentResult.exists();
  }

}
