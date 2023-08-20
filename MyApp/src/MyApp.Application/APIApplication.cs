// MyApp.Application/Interfaces/IUserService.cs
public interface IUserService
{
    Task CreateUserAsync(string username, string email);
}

// MyApp.Application/Services/UserService.cs
public class UserService : IUserService
{
    // Inject necessary repositories or services

    public async Task CreateUserAsync(string username, string email)
    {
        // Perform business logic, create user, etc.
    }
}
