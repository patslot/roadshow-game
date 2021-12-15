import { Component, Renderer2, ElementRef, OnInit, AfterViewInit, ViewChild } from '@angular/core';
import { Observable, Subscription } from 'rxjs';

import { GameService } from '../game.service' ;

@Component({
  selector: 'app-stage4',
  templateUrl: './stage4.component.html',
  styleUrls: ['./stage4.component.scss']
})
export class Stage4Component implements OnInit, AfterViewInit {
  @ViewChild('popContainer') d1:ElementRef;
  @ViewChild('pop1') p1:ElementRef;
  @ViewChild('pop2') p2:ElementRef;
  @ViewChild('pop3') p3:ElementRef;
  @ViewChild('pop4') p4:ElementRef;
  @ViewChild('pop5') p5:ElementRef;
  @ViewChild('pop6') p6:ElementRef;
  @ViewChild('pop7') p7:ElementRef;
  @ViewChild('pop8') p8:ElementRef;
  appleCount: number = 0;
  appleClickCount: number = 0;
  appleInterval  = null;
  showModal: boolean = false;
  appleSlot: string[] = ["p1","p2","p3","p4","p5","p6","p7","p8"];
  RandomAppleSlot: number[] = [];
  prize: string = '' ;
  constructor(
    private renderer: Renderer2,
    private el: ElementRef,
    private gameSerice: GameService) { }

  private getRandomInt() {
    return Math.floor(Math.random() * Math.floor(8));
  }
  ngOnInit(): void {
    this.RandomAppleSlot = this.shuffle(this.appleSlot);
  }
  ngAfterViewInit() {

     this.appleInterval = setInterval( () =>{
        if(this.appleCount <= 8){
          this.addPopUp();
        }else{
          clearInterval(this.appleInterval);
        }
        this.appleCount = this.appleCount + 1;
      },500);

  }
  private shuffle(array) {
    var currentIndex = array.length, temporaryValue, randomIndex;

    // While there remain elements to shuffle...
    while (0 !== currentIndex) {

      // Pick a remaining element...
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex -= 1;

      // And swap it with the current element.
      temporaryValue = array[currentIndex];
      array[currentIndex] = array[randomIndex];
      array[randomIndex] = temporaryValue;
    }

    return array;
  }
  private getAppleDiv(randomslot){
       switch(randomslot) {
          case 'p1': {
            return this.p1.nativeElement;
            break;
          }
          case 'p2': {
            return this.p2.nativeElement;
            break;
          }
          case 'p3': {
            return this.p3.nativeElement;
            break;
          }
          case 'p4': {
            return this.p4.nativeElement;
            break;
          }
          case 'p5': {
            return this.p5.nativeElement;
            break;
          }
          case 'p6': {
            return this.p6.nativeElement;
            break;
          }
          case 'p7': {
            return this.p7.nativeElement;
            break;
          }
          case 'p8': {
            return this.p8.nativeElement;
            break;
          }
          default: {
            break;
          }
       }
  }
  private addPopUp(){
    if(this.RandomAppleSlot.length>0){
      const div = this.getAppleDiv(this.RandomAppleSlot.pop());
      const img = this.renderer.createElement('img');
      img.src = "./assets/apple.png";
      this.renderer.appendChild(div, img);
      this.renderer.appendChild(this.d1.nativeElement, div)
    }

  }
  public onPopClick(e) : void{
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.disabled = true;
    // console.log(this.appleClickCount);
    let element = e.target;
    element.remove();
    this.appleClickCount += 1;
    if(this.appleClickCount == 8){
      clearInterval(this.appleInterval);
      this.showPrize();
    }
  }
  public showPrize() : void{
    this.showModal = true;
    let gift = this.gameSerice.getQuota();
    console.log(gift);
    let proper = Math.random() ;
    console.log(proper);
    let gotPrize = (proper >= 0.5)? true : false ;
    if(gotPrize){
      let tempPrize = Math.floor(Math.random() * Math.floor(3))  ;
      console.log(tempPrize);
      while(gift[tempPrize].Quota<=0){
        tempPrize = Math.floor(Math.random() * Math.floor(3))  ;
        console.log(tempPrize);
      }
      this.prize = gift[tempPrize].Name ;
    }else{
      this.prize = "0";
    }
  }
  onClickNextStage() {
    if(this.prize!='0'){
      this.gameSerice.setPrize(this.prize);
      this.gameSerice.nextStage();
    }
  }
}
