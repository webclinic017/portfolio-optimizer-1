import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "portfolio_optimizer.app:create_app",
        factory=True,
        host="0.0.0.0",
        port=5000,
        reload=True,
    )
