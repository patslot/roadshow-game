import { Component, OnDestroy, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Subscription } from 'rxjs';
import { GameService } from './game.service';
import { Quota } from './quota.model'
import { environment } from '../environments/environment';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnDestroy{
  stage:number;
  quota : Quota[];
  private stageUpdate: Subscription;
  private quotaUpdate: Subscription;

  constructor(
    private gameService: GameService,
    private http: HttpClient
    ){}

  ngOnInit(){
    this.http.get<any>(environment.backend + 'quota').subscribe(data => {
      if(data.status == "SUCCESS"){
        console.log(data)
        this.gameService.setQuota(data.data);
         if ((data.data[0].quota == 0) && (data.data[1].quota == 0) && (data.data[2].quota == 0)){
          this.stage = 7 ;
        }
      }else{
        this.stage = 7;
      }

      console.log(data.status);
        // if ((data[0].quota == 0) && (data[1].quota == 0) && (data[2].quota == 0)){
        //   this.stage = 6 ;
        // }
    })
    this.stage = this.gameService.getStage();
    this.stageUpdate = this.gameService.stageUpdate
      .subscribe(
        (stage: number) =>{
          this.stage = stage;
        }
      )
    this.quotaUpdate = this.gameService.quotaUpdate
        .subscribe(
          (quota:Quota[]) =>{
            this.quota = quota ;
          }
        )
  }

  ngOnDestroy(){
    this.stageUpdate.unsubscribe();
    this.quotaUpdate.unsubscribe();
  }

}
