import { Component, OnInit } from '@angular/core';

import { GameService } from '../game.service' ;
import {Quota} from '../quota.model';

@Component({
  selector: 'app-stage1',
  templateUrl: './stage1.component.html',
  styleUrls: ['./stage1.component.scss']
})


export class Stage1Component implements OnInit {

  constructor(
    private gameSerice: GameService,
  ) {

   }

  ngOnInit(): void {
    console.log(this.gameSerice.getQuota());
  }

  onClickNextStage() {
    this.gameSerice.nextStage();
  }

}
