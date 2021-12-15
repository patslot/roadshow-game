import { Component, OnInit } from '@angular/core';

import { HttpClient } from '@angular/common/http';
import { Subscription } from 'rxjs';

import { GameService } from '../game.service' ;
import {Quota} from '../quota.model';

import { environment } from '../../environments/environment';

@Component({
  selector: 'app-stage2',
  templateUrl: './stage2.component.html',
  styleUrls: ['./stage2.component.scss']
})
export class Stage2Component implements OnInit {
  showModal : boolean = false;
  quotas : Quota[] = [];
  quotaReady : boolean = false;
  emailDulpicated : boolean = false;
  userEmail : string = '';
  emailWrong : boolean = false;
  private quotaUpdate: Subscription;

  constructor(
    private gameSerice: GameService,
    private http:HttpClient
  ) { }

  ngOnInit(): void {
    this.quotaUpdate = this.gameSerice.quotaUpdate
      .subscribe(
        (quota:Quota[]) =>{
          this.quotas = quota ;
          console.log(this.quotas );
          this.quotaReady = true;
        }
      )

  }
  validateEmail(email) : boolean{
    let re = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/
    if (re.test(email)) {
      return true
    }else{
      return false
    }
  }
  checkDulpicateEmail(email) {
    const formData = new FormData();
    formData.append('email', email);
    this.http.post<any>( environment.backend + 'checkemail', formData).toPromise()  .then(res => {
      if(res.status == "SUCCESS"){
        this.emailDulpicated = false;
      }else{
        this.emailDulpicated = true;
      }
    })

  }

  submitUser(email){
    const formData = new FormData();
    formData.append('email',email);
    this.http.post<any>(environment.backend + 'submituser',  formData).subscribe({
        next: data => {
           console.log(data);
        },
        error: error => {
          console.log(error);
        }
    })
  }

  onClickNextStage() {
    console.log(this.userEmail);
    if(this.validateEmail(this.userEmail)){
      this.gameSerice.checkDulpicateEmail(this.userEmail).subscribe(response => {
        console.log(response);
        if (response.status=="SUCCESS"){
          this.emailWrong = false;
          this.submitUser(this.userEmail);
          this.gameSerice.setEmail(this.userEmail);
          this.gameSerice.nextStage();
        }else{
          if (response.status=="DULIPICATE"){
           this.emailDulpicated = true ;
          }
        }
      })

    }else{
      this.emailWrong = true;
    }
  }
  onClickModalActive(){
    this.showModal = true ;
  }
}
