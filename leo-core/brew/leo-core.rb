require "language/python/virtualenv"

class LeoCore < Formula
  include Language::Python::Virtualenv

  desc "AI visibility scoring engine"
  homepage "https://github.com/leo-labs/leo-core"
  url "https://github.com/leo-labs/leo-core/archive/refs/tags/v0.2.0.tar.gz"
  sha256 "0" * 64
  license "MIT"

  depends_on "python@3.11"

  def install
    virtualenv_install_with_resources
    pkgshare.install "brew/postinstall.sh"
  end

  def post_install
    ohai "Configuring Leo Core"
    system "bash", "#{pkgshare}/postinstall.sh"
  end

  test do
    system bin/"leo", "--help"
  end
end
