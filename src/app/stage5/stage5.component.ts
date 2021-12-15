import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { GameService } from '../game.service';

import { HttpClient } from '@angular/common/http';

import { environment } from '../../environments/environment';


@Component({
  selector: 'app-stage5',
  templateUrl: './stage5.component.html',
  styleUrls: ['./stage5.component.scss']
})
export class Stage5Component implements OnInit {
  userName: string = "";
  userCompany: string = "";
  userEmail: string ="";
  userPrize: string = "" ;
  formprocessing: boolean = false ;
  constructor(
    private gameSerice: GameService,
    private http:HttpClient
    ) { }

  ngOnInit(): void {
    this.userEmail = this.gameSerice.getEmail();
    this.userPrize = this.gameSerice.getPrize();
  }
  onClickSubmit(form: NgForm){
    this.formprocessing = true;
    const formData = new FormData();
    formData.append('name', this.userName);
    formData.append('company', this.userCompany);
    formData.append('email', this.userEmail);
    formData.append('option',this.userPrize);


    this.http.post<any>(environment.backend + 'submit',  formData).subscribe({
        next: data => {

           if(data.status=="SUCCESS"){
             this.gameSerice.gotoStage(6);
           }else{
             this.gameSerice.gotoStage(7);
           }
        },
        error: error => {
          console.log(error);
        }
    })
  }
}
