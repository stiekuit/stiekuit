public void ConfigureServices(IServiceCollection services)
{
    // ...

    services.AddScoped<IUserService, UserService>();
    services.AddScoped<IUserRepository, UserRepository>();

    // ...
}
// q: how to create a function?