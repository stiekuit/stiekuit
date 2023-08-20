// MyApp.WebApi/Controllers/UserController.cs
[ApiController]
[Route("api/[controller]")]
public class UserController : ControllerBase
{
    private readonly IUserService _userService;

    public UserController(IUserService userService)
    {
        _userService = userService;
    }

    [HttpPost("create")]
    public async Task<IActionResult> CreateUser([FromBody] CreateUserRequest request)
    {
        // Perform validation if needed

        await _userService.CreateUserAsync(request.Username, request.Email);

        return Ok(new { Message = "User created successfully." });
    }
}
