export interface Job {
  title: string;
  description: string;
  href: string;
  location: {
    country: string;
    city: string;
  };
  company: {
    name: string;
    url: string;
    logo: string;
  };
}
