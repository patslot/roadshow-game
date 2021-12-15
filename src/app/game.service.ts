import { HttpClient } from '@angular/common/http';
import { Injectable, OnInit } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { Quota } from './quota.model'

import { environment } from '../environments/environment';

@Injectable()
export class GameService {
  stageUpdate = new Subject<number>();
  quotaUpdate = new Subject<Quota[]>();
  userEmail: string = '';
  userPrize: string = '' ;

  constructor(private http:HttpClient) { }

  private stage:number = 1;
  private quotas : Quota[] = [];
  setPrize(Prize){
    this.userPrize = Prize ;
  }
  getPrize(){
    return this.userPrize ;
  }
  setEmail(email){
    this.userEmail = email ;
  }
  getEmail(){
    return this.userEmail ;
  }
  setQuota(quotas) {
    quotas.forEach(quota => {
      this.quotas.push(new Quota(
        quota.Date,
        quota.Giftid,
        quota.name,
        quota.quota
        ));
    });
    console.log(this.quotas);
    this.quotaUpdate.next(this.quotas);
  }
  getQuota(){
    return this.quotas.slice();
  }
  getStage() {
    return this.stage ;
  }
  gotoStage(i){
    this.stage = i;
    this.stageUpdate.next(this.stage) ;
  }
  nextStage() {
    this.stage = this.stage + 1;
    this.stageUpdate.next(this.stage) ;
  }
  checkDulpicateEmail(email) :Observable<any> {
    const formData = new FormData();
    formData.append('email', email);
    return this.http.post<any>(environment.backend + 'checkemail', formData)
  }
}
