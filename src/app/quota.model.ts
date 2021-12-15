export class Quota {
  public Date: string;
  public Giftid: number;
  public Name: string;
  public Quota: number;
  constructor(Date: string, Giftid: number, Name: string, Quota: number) {
    this.Date = Date;
    this.Giftid = Giftid;
    this.Name = Name;
    this.Quota = Quota;
  }
}
