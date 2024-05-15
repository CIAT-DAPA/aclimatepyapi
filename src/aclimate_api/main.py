from geographic import Geographic

def main():
    g = Geographic("https://webapi.aclimate.org/api/")
    print(g.get_geographic("636c0813e57f2e6ac61394e6"))

if __name__ == "__main__":
    main()