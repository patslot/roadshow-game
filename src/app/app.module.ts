import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { AppComponent } from './app.component';
import { Stage1Component } from './stage1/stage1.component';
import { Stage2Component } from './stage2/stage2.component';
import { Stage3Component } from './stage3/stage3.component';
import { Stage4Component } from './stage4/stage4.component';
import { Stage5Component } from './stage5/stage5.component';
import { Stage6Component } from './stage6/stage6.component';
import { Stage7Component } from './stage7/stage7.component';
import { GameService } from './game.service';

@NgModule({
  declarations: [
    AppComponent,
    Stage1Component,
    Stage2Component,
    Stage3Component,
    Stage4Component,
    Stage5Component,
    Stage6Component,
    Stage7Component
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [GameService],
  bootstrap: [AppComponent]
})
export class AppModule { }
