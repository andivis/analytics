function MakeRegex() {
  var maximumRegexLength = 7000;
  
  var range = SpreadsheetApp.getActiveSheet().getRange('A:B');
  
  var numRows = SpreadsheetApp.getActiveSheet().getMaxRows();
  
  var currentRow = '';
  var currentOutputRow = 1;
  
  for (var i = 1; i <= numRows; i++) {
    var currentValue = range.getCell(i,1).getValue();
    
    if(!currentValue)
    {
      continue;
    }
    
    var regex = getAfterDomain_(currentValue);
    regex = escapeRegExp_(regex);
    
    if(regex.length >= maximumRegexLength)
    {
      Logger.log('Skipping row ' + i + '. Regex is too long for this url.');
      continue;
    }
    
    if(currentValue && currentRow.length + regex.length >= maximumRegexLength)
    {
      //remove extra character if needed
      if(currentRow && currentRow.slice(-1) === '|' && currentRow.slice(-2) !== '\|')
      {
        currentRow = currentRow.slice(0, -1);
      }
      
      //end this row
      Logger.log('\nWill send this regex: ' + currentRow + '\n')
      
      range.getCell(currentOutputRow, 2).setValue(currentRow);
      currentOutputRow++;
      
      //start a new row
      currentRow = regex;
    }      
    else if(currentValue)
    {
      //add to current row
      currentRow += regex;
    }
    
    //not last?
    if(currentValue && i < numRows - 2)
    {
      currentRow += '|';
    }
  }
  
  //output any remaining ones
  if(currentRow)
    {
      //remove extra character if needed
      if(currentRow && currentRow.slice(-1) === '|' && currentRow.slice(-2) !== '\|')
      {
        currentRow = currentRow.slice(0, -1);
      }

      Logger.log('\nWill send this regex: ' + currentRow + '\n');
      
      range.getCell(currentOutputRow, 2).setValue(currentRow);
      currentOutputRow++;
    }
}

function getAfterDomain_(url)
{
  result = '';
   
  fields = url.split('/');
  for (var i = 3; i < fields.length; i++) {
    result += fields[i];
    
    if(i < fields.length - 1)
    {
      result += '/';
    }
  }
  
  if(result && result[result.length - 1] === '/')
  {
    result = result.substring(0, result.length - 1);
  }
  
  return result;
}

function escapeRegExp_(string) {
  return string.replace(/[.*+?^${}()\-|[\]\\]/g, '\\$&'); // $& means the whole matched string
}