var c = localStorage.getItem('theme');

if(c == 'dark')
{
  DarkReader.enable({
  brightness: 100,
  contrast: 100,  
  });
}

function toggle() {
  var a = DarkReader.isEnabled();
  if (a == true) {
    DarkReader.disable();
    localStorage.setItem("theme", 'light');
    a = false;
  } 
  else {
    DarkReader.enable({
    brightness: 100,
    contrast: 100,  
    });
    localStorage.setItem('theme', 'dark');
    a = true;
  }
}

// const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
// const currentTheme = sessionStorage.setItem('data-theme', 'light');

// if (currentTheme) 
// {
//     document.documentElement.setAttribute('data-theme', currentTheme);
  
//     if (currentTheme === 'dark') 
//     {
//         toggleSwitch.checked = true;
//     }
// }

// function switchTheme(e) 
// {
//     if (e.target.checked) 
//     {
//       document.documentElement.setAttribute('data-theme', 'dark');
//       DarkReader.enable({
//       brightness: 100,
//       contrast: 100,  
//       });
//     }
//     else 
//     {        
//       document.documentElement.setAttribute('data-theme', 'light');
//       DarkReader.disable();
//     }    
// }

// toggleSwitch.addEventListener('change', switchTheme, false);