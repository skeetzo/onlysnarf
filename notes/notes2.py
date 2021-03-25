# https://crossbrowsertesting.com/blog/selenium/selenium-design-patterns/


import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.CacheLookup;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.How;

public class LoginPage {

@FindBy(how = How.ID, using = "username")
@CacheLookup
private WebElement username;

@FindBy(how = How.ID, using = "password")
@CacheLookup
private WebElement password;

@FindBy(how = How.ID, using = "login")
@CacheLookup
private WebElement login;

public String GetUsername() {

return username.getAttribute("value");>/pre>

}

public void setUsername(String value) {

username.clear();
username.sendKeys(value);

}

public String getPassword() {

return password.getAttribute("value");

}

public void setPassword(String value) {

password.clear();
password.sendKeys(value);

}

public void submitLogin() {

login.click();

}

}
















import org.junit.Test;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.PageFactory;

public class LoginTest {

@Test
public void testLogin() {

WebDriver driver = new ChromeDriver();

driver.navigate().to("http://www.selenium.academy/Examples/DesignPattern.html");

// Create a new instance of the login page object
LoginPage login = PageFactory.initElements(driver, LoginPage.class);

// set the username
login.setUsername("daniel");

// set the password
login.setPassword("secret");

// submit the login
login.submitLogin();

driver.quit();

}

}