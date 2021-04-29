function get()
{
  console.log("Hi")
  console.log(i.amount)
  var amountf=0.0;
  for (i in datap)
  {
    /*if (i.amount<0)
    {
      amountf=i.amount*(1.0);
    }
    else if(i.amount>=0)
    {
      amountf=i.amount*(-1.0);
    } */
    amountf=i.amount
  }

  document.getElementById("myAmount").innerHTML = amountf;
}
