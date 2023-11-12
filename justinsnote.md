```html
<table class="performance-facts__table">
              <thead>
                <tr>
                  <th colspan="3" class="amps">Amount Per Serving</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th colspan="2" id="lkcal-val-cal"><b>Calories</b></th>
                  <td class="nob">{{ recipe.nutrition_label.calories }} </td>
                </tr>
             
                <tr>
                  <!-- <th colspan="2"><b>Total Fat</b>{ recipe.nutrition_label.total_fat }}</th> -->
                </tr>
                <tr>
                  <td class="blank-cell"></td>
                  <!-- <th><b>Saturated Fat</b> { recipe.nutrition_label.saturated_fat }}</th> -->
                
                </tr>
                <tr>
                  <td class="blank-cell"></td>
                  <!-- <th><b>Trans Fat</b> { recipe.nutrition_label.trans_fat }}</th> -->
              
                </tr>
                <tr>
                  <!-- <th colspan="2"><b>Cholesterol</b>{ recipe.nutrition_label.cholesterol }}</th> -->
                
                </tr>
                <tr>
                  <!-- <th colspan="2"><b>Sodium</b> { recipe.nutrition_label.sodium }}</th> -->
                 
                </tr>
                <tr>
                  <!-- <th colspan="2"><b>Total Carbohydrate</b> { recipe.nutrition_label.total_carbs }}</th> -->
                  
                </tr>
                <tr>
                  <td class="blank-cell"></td>
                  <!-- <th><b>Dietary Fiber</b> { recipe.nutrition_label.dietary_fiber }}</th> -->
                </tr>
                <tr>
                  <td class="blank-cell"></td>
                  <!-- <th><b>Total Sugars</b> { recipe.nutrition_label.total_sugars }}</th> -->
             
                </tr>
                <tr>
                  <td class="blank-cell"></td>
                  <!-- <th><b>Added Sugars</b> { recipe.nutrition_label.added_sugars }}</th> -->
        
                </tr>
                <tr class="thick-end">
                  <!-- <th colspan="2"><b>Protein</b> { recipe.nutrition_label.protein }}</th> -->
               
                </tr>
              </tbody>
            </table>
```


```html
 <table class="performance-facts__table">
              <thead>
                <tr>
                  <th colspan="3" class="amps">Amount Per Serving</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th colspan="2" id="lkcal-val-cal"><b>Calories</b></th>
                  <td class="nob">{{ recipe.nutrition_label.calories }} </td>
                </tr>
             
                <tr>
                  <th colspan="2"><b>Total Fat</b>{{ recipe.nutrition_label.total_fat }}</th>
                </tr>
                <tr>
                  <td class="blank-cell"></td>
                  <th><b>Saturated Fat</b> {{ recipe.nutrition_label.saturated_fat }}</th>
                
                </tr>
                <tr>
                  <td class="blank-cell"></td>
                  <th><b>Trans Fat</b> {{ recipe.nutrition_label.trans_fat }}</th>
              
                </tr>
                <tr>
                  <th colspan="2"><b>Cholesterol</b>{{ recipe.nutrition_label.cholesterol }}</th>
                
                </tr>
                <tr>
                  <th colspan="2"><b>Sodium</b> {{ recipe.nutrition_label.sodium }}</th>
                 
                </tr>
                <tr>
                  <th colspan="2"><b>Total Carbohydrate</b> {{ recipe.nutrition_label.total_carbs }}</th>
                  
                </tr>
                <tr>
                  <td class="blank-cell"></td>
                  <th><b>Dietary Fiber</b> {{ recipe.nutrition_label.dietary_fiber }}</th>
                </tr>
                <tr>
                  <td class="blank-cell"></td>
                  <th><b>Total Sugars</b> {{ recipe.nutrition_label.total_sugars }}</th>
             
                </tr>
                <tr>
                  <td class="blank-cell"></td>
                  <th><b>Added Sugars</b> {{ recipe.nutrition_label.added_sugars }}</th>
        
                </tr>
                <tr class="thick-end">
                  <th colspan="2"><b>Protein</b> {{ recipe.nutrition_label.protein }}</th>
               
                </tr>
              </tbody>
            </table>
```