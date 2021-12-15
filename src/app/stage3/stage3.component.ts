import { Component, ElementRef, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { GameService } from '../game.service';

@Component({
  selector: 'app-stage3',
  templateUrl: './stage3.component.html',
  styleUrls: ['./stage3.component.scss']
})
export class Stage3Component implements OnInit {
  optionA:string='./assets/s3_a.png';
  optionB:string='./assets/s3_b.png';
  optionC:string='./assets/s3_c.png';
  optionD:string='./assets/s3_d.png';
  optionE:string='./assets/s3_e.png';
  optionAON:string='./assets/s3_a_on.png';
  optionBON:string='./assets/s3_b_on.png';
  optionCON:string='./assets/s3_c_on.png';
  optionDON:string='./assets/s3_d_on.png';
  optionEON:string='./assets/s3_e_on.png';
  option:string = '';
  wrong: boolean = false;
  constructor(
    private gameSerice: GameService
  ) { }

  ngOnInit(): void {
  }
  onSetOption(e){
    this.option = e ;
  }
  onClickNextStage() {
    this.gameSerice.nextStage();
  }
  onClickSubmitAnswer(form: NgForm){
    if(this.option != ""){
      console.log(form.value.question);
      if(form.value.question == 5){
        this.gameSerice.gotoStage(4)
      }else{
        this.wrong = true ;
      }
    }else{
      alert('請選擇其中一個答案')
    }
  }
}
